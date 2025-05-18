using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Entities.Interfaces;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Device : MainEntity , IHasCompany
{
    [Required] [MaxLength(255)]
    public string Name { get; set; }
    public string? SerialNo { get; set; }
    public Guid CompanyId { get; set; }
    public Guid? ProjectId { get; set; }


    [ForeignKey("CompanyId")] public Company Company { get; set; } = null!;

    [ForeignKey("ProjectId")] public Project? Project { get; set; } = null!;

}