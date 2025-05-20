using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class PunchLog : MainEntity , IHasCompany
{
    public Guid EmployeeId { get; set; }
    public Guid? DeviceId { get; set; }
    public Guid CompanyId { get; set; }
    public Guid SiteId { get; set; }
    public Guid ProjectId { get; set; }
    
    public double Latitude { get; set; }
    public double Longitude { get; set; }
    public string? ImgSrc { get; set; }

    public DateTime PunchDateTime { get; set; }
    public PunchType PunchType { get; set; }

    public Employee Employee { get; set; } =  null!;
    public Device? Device { get; set; }
    public Company Company { get; set; } =  null!;
    [ForeignKey("SiteId")]
    public Site Site { get; set; } =  null!;
    public Project Project { get; set; } =  null!;
}