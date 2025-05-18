using System.ComponentModel.DataAnnotations;
using BuildingBlock.Core.Domain.Abstractions;
using RSG.Biovision.Domain.Enums;

namespace RSG.Biovision.Domain.Entities;

public class Site : MainEntity
{
    [MaxLength(255)]
    public string? NameAr { get; set; }

    [Required]
    [MaxLength(255)]
    public string NameEn { get; set; } = null!;

    public double? Latitude { get; set; }
    public double? Longitude { get; set; }
    public double? Radius { get; set; }
    
    public string? Location { get; set; }
    
    public Guid ProjectId { get; set; }
    
    public Project? Project { get; set; }
    public ICollection<EmployeeSite> EmployeeSites { get; set; } = new List<EmployeeSite>();

   
}