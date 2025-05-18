using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace RSG.Biovision.Domain.Entities;

public class ProjectSite : MainEntity
{
    [Required]
    public Guid ProjectId { get; set; }
    
    [Required]
    [Column(TypeName = "decimal(10, 6)")]
    public decimal Latitude { get; set; }
    
    [Required]
    [Column(TypeName = "decimal(10, 6)")]
    public decimal Longitude { get; set; }
    
    [Column(TypeName = "decimal(10, 2)")]
    public decimal? Radius { get; set; }
    
    [MaxLength(255)]
    public string? Name { get; set; }
    
    [MaxLength(500)]
    public string? Description { get; set; }
    
    // Navigation property
    [ForeignKey("ProjectId")] public virtual Project Project { get; set; } = null!;
}